import sys

import uvicorn

if __name__ == '__main__':
    for path in sys.path:
        print(path)

    uvicorn.run(
        app="app.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
