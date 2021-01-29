import a_star_search

node_connections = [
    [1,5],[0,2,6],[1,3],[2,4,8],[3,9],
    [0,10],[1,7],[6,12],[3,13],[4,14],
    [5,11],[10,16],[7,13],[8,12,14,18],[9,13],
    [16,20],[11,15,17],[16,22],[13,19],[18,24],
    [15,21],[20,22],[17,21,23],[22,24],[19,23]
    ]


node_positions = [
    [0,0],[1,0],[2,0],[3,0],[4,0],
    [0,1],[1,1],[2,1],[3,1],[4,1],
    [0,2],[1,2],[2,2],[3,2],[4,2],
    [0,3],[1,3],[2,3],[3,3],[4,3],
    [0,4],[1,4],[2,4],[3,4],[4,4]
    ]

print(a_star_search.a_star_search(node_positions, node_connections, 6, 22))
