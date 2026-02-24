<template>
  <div class="container mt-4">
    <h3 class="mb-4">📰 求职资讯</h3>
    <div class="row">
      <div class="col-md-8">
        <div class="card mb-3 border-0 shadow-sm" v-for="i in 5" :key="i">
          <div class="card-body">
            <h5 class="card-title fw-bold text-primary">2026年高校毕业生就业形势分析报告</h5>
            <p class="card-text text-muted">随着经济复苏，各行各业对人才的需求发生了深刻变化，本文将深入剖析...</p>
            <small class="text-muted">发布于 2026-03-15 • 阅读 1024</small>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-light border-0 p-3">
          <h5>热门话题</h5>
          <ul class="list-unstyled mt-2">
            <li class="mb-2"><a href="#" class="text-decoration-none text-dark">#春招攻略</a></li>
            <li class="mb-2"><a href="#" class="text-decoration-none text-dark">#简历优化技巧</a></li>
            <li class="mb-2"><a href="#" class="text-decoration-none text-dark">#面试常见问题</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>