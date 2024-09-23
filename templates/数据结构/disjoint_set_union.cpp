struct DSU {
    int n;
    vector<int> fa, siz;

    DSU(int n) : n(n) {
        init(n);
    }

    void init(int n) {
        fa.resize(n);
        iota(fa.begin(), fa.end(), 0);
        siz.assign(n, 1);
    }

    int find(int x) {return (x == fa[x] ? x : fa[x] = find(fa[x]));}

    bool merge(int x, int y) {
        int fx = find(x), fy = find(y);
        if (fx == fy) return false;
        fa[fy] = fx;
        siz[fx] += siz[fy];
        return true;
    }

    bool same(int x, int y) {
        return find(x) == find(y);
    }
};