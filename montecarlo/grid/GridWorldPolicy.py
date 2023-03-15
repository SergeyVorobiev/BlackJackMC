from montecarlo.grid.Cell import Cell


def update_policy_colors(cells, values, cell_value_func):
    uniques = len(set(values))
    step = 255 / uniques
    r = 10
    value = None
    for cell in cells:
        cell: Cell = cell
        cell_v = cell_value_func(cell)
        if value != cell_v:
            r += step
            value = cell_v
        color = int(min(r + 20, 255))
        if not cell.is_target:
            #cell.set_default_color(0, 0 + int(color / 1), 0 + int(color / 1))
            cell.set_default_color(255 - color, color, 255 - color)
            cell.reset_color()


def update_policy_colors_cells(cells, cell_value_func):
    cells, values = get_sorted_by_value_cells(cells, cell_value_func)
    update_policy_colors(cells, values, cell_value_func)


def update_policy_colors_grid(grid, cell_value_func):
    cells, values = get_sorted_by_value_grid(grid, cell_value_func)
    update_policy_colors(cells, values, cell_value_func)


def get_sorted_by_value_cells(cells, cell_value_func):
    cells_t = []
    values = []
    for cell in cells:
        cell: Cell = cell
        cells_t.append(cell)
        values.append(cell_value_func(cell))
    return sorted(cells_t, key=lambda cell: cell_value_func(cell), reverse=False), values


def get_sorted_by_value_grid(grid, cell_value_func):
    cells = []
    values = []
    for row in grid:
        for cell in row:
            cell: Cell = cell
            cells.append(cell)
            values.append(cell_value_func(cell))
    return sorted(cells, key=lambda cell: cell_value_func(cell), reverse=False), values
