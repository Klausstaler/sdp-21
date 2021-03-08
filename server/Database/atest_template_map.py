import a_star_search

node_positions = [
    [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0]],#0
    [[0,1],[0.5,1],[2.5,1],[3,1],[3.5,1],[5.5,1],[6,1],[6.5,6],[8.5,1],[9,1]],#10
    [[0,2],[0.5,2],[2.5,2],[3,2],[3.5,2],[5.5,2],[6,2],[6.5,6],[8.5,2],[9,2]],#20
    [[0,3],[0.5,3],[2.5,3],[3,3],[3.5,3],[5.5,3],[6,3],[6.5,6],[8.5,3],[9,3]],#30
    [[0,4],[0.5,4],[2.5,4],[3,4],[3.5,4],[5.5,4],[6,4],[6.5,6],[8.5,4],[9,4]],#40
    [[0,5],[0.5,5],[2.5,5],[3,5],[3.5,5],[5.5,5],[6,5],[6.5,6],[8.5,5],[9,5]],#40
    [[0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6],[7,6],[8,6],[9,6]]
    ]

node_connections = [
    [1],[2],[3],[4,13],[5],[6],[7],[8],[9],[19],
    [0,11],[10],[13],[12,14,23],[13],[16],[6,15,17],[16],[19],[18,29],
    [10,21],[20],[23],[22,24,33],[23],[26],[16,25,27],[26],[29],[28,39],
    [20,31],[30],[33],[32,34,43],[33],[36],[26,35,37],[36],[39],[38,49],
    [30,41],[40],[43],[42,44,53],[43],[46],[36,45,47],[46],[49],[48,59],
    [40,51],[50],[53],[52,54,63],[53],[56],[46,55,57],[56],[59],[58,69],
    [50],[60],[61],[62],[63],[64],[65,56],[66],[67],[68],
    ]


node_distances = [
    [1],[1],[1],[1,1],[1],[1],[1],[1],[1],[1],
    [1,1],[1],[1],[1,1,1],[1],[1],[1,1,1],[1],[1],[1,1],
    [1,1],[1],[1],[1,1,1],[1],[1],[1,1,1],[1],[1],[1,1],
    [1,1],[1],[1],[1,1,1],[1],[1],[1,1,1],[1],[1],[1,1],
    [1,1],[1],[1],[1,1,1],[1],[1],[1,1,1],[1],[1],[1,1],
    [1,1],[1],[1],[1,1,1],[1],[1],[1,1,1],[1],[1],[1,1],
    [1],[1],[1],[1],[1],[1],[1,1],[1],[1],[1],
    ]

print(a_star_search.a_star_search(node_positions, node_connections, node_distances, 1, 41))
