import aiohttp


async def _make_matrix(body: str) -> list[list[int]]:
    """Makes matrix from given text"""
    matrix_list = body.strip().replace('|', '').split('\n')
    matrix = [list(map(int, matrix_list[line].strip().split())) 
              for line in range(1, len(matrix_list), 2)]    

    return matrix


async def _load_matrix(url: str) -> list[list[int]]:
    """Loads matrix from a server(by protocol HTTP(S))"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            matrix = await _make_matrix(await response.text())
                
    return matrix


async def _matrix_bypass(matrix: list[list[int]]) -> list[int]:
    """Returns bypassed matrix by spiral"""
    new_matrix = []
    top = left = direction = 0
    down = len(matrix) - 1
    right = len(matrix[0]) -1

    while (top <= down and left <= right):
        match direction:
            case 0:
                [new_matrix.append(matrix[i][left]) for i in range(top, down + 1)]
                left += 1
                direction = 1
            case 1:
                [new_matrix.append(matrix[down][i]) for i in range(left, right + 1)]
                down -= 1
                direction = 2
            case 2:
                [new_matrix.append(matrix[i][right]) for i in range(down, top - 1, -1)]
                right -= 1
                direction = 3
            case 3:
                [new_matrix.append(matrix[top][i]) for i in range(right, left - 1, -1)]
                top += 1
                direction = 0

    return new_matrix



async def get_matrix(url: str) -> list[int]:
    """Returns processed matrix"""
    matrix = await _load_matrix(url)
    bypassed_matrix = await _matrix_bypass(matrix)
    print(bypassed_matrix)

    return bypassed_matrix
