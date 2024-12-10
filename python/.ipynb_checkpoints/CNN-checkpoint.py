

def heuristic_search(max_depth):
    best_move = None
    best_score = float('-inf')
    threat_moves = find_threat_moves()  # 找到对手棋子形成威胁较大的区域周边的落子位置
    if threat_moves:
        for move in threat_moves:
            make_move(move)
            score = get_evaluate()
            undo_move(move)
            if score > best_score:
                best_score = score
                best_move = move
    else:
        for depth in range(1, max_depth + 1):
            score, move = alpha_beta_search_with_heuristic(depth)
            if score > best_score:
                best_score = score
                best_move = move
    return best_move

def alpha_beta_search_with_heuristic(depth, alpha, beta):
    if depth == 0 or game_over():
        return get_evaluate(), None
    legal_moves = get_legal_moves()
    sorted_moves = sort_moves_by_heuristic(legal_moves)  # 根据启发式信息对合法落子位置进行排序
    best_move = None
    for move in sorted_moves:
        make_move(move)
        score, _ = alpha_beta_search_with_heuristic(depth - 1, alpha, beta)
        undo_move(move)
        if score > alpha:
            alpha = score
            best_move = move
        if alpha >= beta:
            break
    return alpha, best_move

def find_threat_moves():
    threat_moves = []
    for r in range(const.board_size_H):
        for c in range(const.board_size_W):
            if is_threat_area(r, c):  # 判断 (r, c) 位置是否处于对手威胁区域
                threat_moves.append((r, c))
    return threat_moves

def is_threat_area(r, c):
    # 这里可以通过判断对手棋子在该位置周边形成的棋型、数量等情况来确定是否为威胁区域
    # 例如，如果对手棋子在某个方向上形成活三、冲四等情况，周边的空白位置可视为威胁区域
    enemy_count = judge(r, c, 1, 2)  # 这里假设judge函数能统计相关棋子情况
    if enemy_count >= 3:  # 简单示例，可根据实际调整
        return True
    return False