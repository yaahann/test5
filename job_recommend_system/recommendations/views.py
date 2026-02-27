import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from jobs.models import Job
from jobs.serializers import JobSerializer
from users.models import JobSeeker


class ContentBasedRecommendationView(APIView):
    # 必须是登录用户才能获取个性化推荐
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1. 安全校验：只有求职者才需要推荐
        if user.role_type != 1:
            return Response({"detail": "非求职者账号，暂无推荐"}, status=400)

        try:
            seeker = JobSeeker.objects.get(user=user)
        except JobSeeker.DoesNotExist:
            return Response({"detail": "求职者资料不完善"}, status=400)

        # 2. 提取并构造“求职者画像文本”
        user_features = [
            seeker.skills or "",
            seeker.education or "",
            seeker.major or "",
            seeker.experience or ""
        ]
        user_text = " ".join(user_features)

        # 如果用户什么都没填，就随便推最新职位（冷启动降级策略）
        if not user_text.strip():
            latest_jobs = Job.objects.filter(status=1).order_by('-create_time')[:10]
            return Response(JobSerializer(latest_jobs, many=True).data)

        # 3. 提取全库在招职位，构造“职位画像文本”
        jobs = Job.objects.filter(status=1)
        if not jobs.exists():
            return Response([])

        job_list = list(jobs)
        job_texts = []
        for job in job_list:
            job_features = [
                job.job_title,
                job.job_tags or "",
                job.description or "",
                job.city,
                job.education_req,
                job.exp_req
            ]
            job_texts.append(" ".join(job_features))

        # 4. 使用 jieba 进行中文分词
        user_words = " ".join(jieba.lcut(user_text))
        job_words_list = [" ".join(jieba.lcut(t)) for t in job_texts]

        # 5. TF-IDF 向量化 + 余弦相似度计算
        corpus = [user_words] + job_words_list
        vectorizer = TfidfVectorizer()

        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
        except ValueError:
            # 容错：如果全库都是生僻词或空字符串导致无法矩阵化
            return Response(JobSerializer(job_list[:10], many=True).data)

        # 计算第0行（求职者）与后续所有行（职位）的相似度得分
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        # 6. 打分、排序并截取 Top 10
        scored_jobs = []
        for i, job in enumerate(job_list):
            score = cosine_sim[i]
            if score > 0.05:  # 设定一个最低阈值，低于 0.05 认为基本不匹配
                # 换算成百分制分数（如 85.5），临时挂载到 job 对象上
                job.match_score = round(score * 100, 1)
                scored_jobs.append((job, score))

        # 按相似度分数降序排列
        scored_jobs.sort(key=lambda x: x[1], reverse=True)
        top_jobs = [item[0] for item in scored_jobs[:10]]

        # 如果经过匹配后一个符合的都没有（说明岗位太少或完全不对口），用最新岗位补齐
        if not top_jobs:
            top_jobs = Job.objects.filter(status=1).order_by('-create_time')[:10]
            for j in top_jobs:
                j.match_score = 0  # 兜底推荐没有匹配分

        # 7. 序列化并手动将 match_score 注入到返回的 JSON 中
        serializer = JobSerializer(top_jobs, many=True)
        data = serializer.data
        for idx, job_data in enumerate(data):
            job_data['match_score'] = getattr(top_jobs[idx], 'match_score', 0)

        return Response(data)
