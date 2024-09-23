struct LCA {
    const int N;
    int n, idx;
    vector<int> id, rid, dep, fa;
    vector<vector<int>> e, st;

    LCA(int n) : N(__lg(n) + 1), n(n), idx(0), id(n, -1), rid(n), dep(n), fa(n), e(n), st(N, vector<int>(n)) {}

    void add(int u, int v) {
        e[u].push_back(v);
        e[v].push_back(u);
    }

    int getMin(int x, int y) {
        return dep[x] < dep[y] ? x : y;
    }

    void dfs(int u) {
        id[u] = idx;
        rid[idx] = u;
        idx++;

        for (int v : e[u]) {
            if (id[v] != -1) {
                continue;
            }

            dep[v] = dep[u] + 1;
            fa[v] = u;
            dfs(v);
        }
    }

    void work(int rt = 0) {
        dep[rt] = 1;
        dfs(rt);

        for (int i = 0; i < n; ++i) {
            st[0][i] = rid[i];
        }

        for (int i = 1; i < N; ++i) {
            for (int j = 0; j + (1 << i) - 1 < n; ++j) {
                st[i][j] = getMin(st[i - 1][j], st[i - 1][j + (1 << (i - 1))]);
            }
        }
    }

    int getLca(int x, int y) {
        if (x == y) {
            return x;
        }
        x = id[x], y = id[y];
        if (x > y) {
            swap(x, y);
        }
        ++x;
        int z = __lg(y - x + 1);
        return fa[getMin(st[z][x], st[z][y - (1 << z) + 1])];
    }
};