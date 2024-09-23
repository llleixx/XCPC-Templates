struct Dinic {
    struct Edge {
        int v;
        LL w;
        Edge(int v, LL w) : v(v), w(w) {}
    };

    int n;
    vector<Edge> edges;
    vector<int> d, cur;
    vector<vector<int>> e;
    Dinic(int n) : n(n), d(n), cur(n), e(n) {}

    void reset(int n) { 
        this->n = n;
        edges.clear();
        e.resize(n), d.resize(n), cur.resize(n);
        for (int i = 0; i < n; ++i) 
            e.clear();
    }

    void add(int u, int v, LL w) {
        e[u].push_back(edges.size());
        edges.emplace_back(v, w);
        e[v].push_back(edges.size());
        edges.emplace_back(u, 0);
    }

    bool bfs(int s, int t) {
        d.assign(n, 0);
        queue<int> q;
        d[s] = 1;
        q.push(s);
        while (q.size()) {
            int u = q.front();
            q.pop();
            for (int i : e[u]) {
                auto [v, w] = edges[i];
                if (w && !d[v]) {  // 有 w 才能保证正确性（能正确回溯）
                    d[v] = d[u] + 1;
                    q.push(v);
                    if (v == t) return 1;
                }
            }
        }
        return 0;
    }

    LL maxFlow(int s, int t) {
        LL maxflow = 0;

        auto dfs = [&](auto &&self, int u, LL flow) -> LL {
            if (u == t) {
                return flow;  // 返回至多能减多少。
            }
            LL rest = flow;
            for (int &i = cur[u]; i < (int)e[u].size(); ++i) {
                int j = e[u][i];
                auto [v, w] = edges[j];
                if (w && d[v] == d[u] + 1) {
                    LL k = self(self, v, min(rest, w));
                    if (!k) d[v] = 0;
                    rest -= k, edges[j].w -= k, edges[j ^ 1].w += k;
                    if (!rest) break;  // 这里 break 才能保证复杂度。
                }
            }
            return flow - rest;
        };

        while (bfs(s, t)) {
            cur.assign(n, 0);
            maxflow += dfs(dfs, s, numeric_limits<LL>::max());
        }

        return maxflow;
    }
};