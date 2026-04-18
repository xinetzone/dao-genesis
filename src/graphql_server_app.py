from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from graphql_schema import schema
import threading
import time

app = FastAPI()

# 添加GraphQL路由
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# 健康检查路由
@app.get('/health')
def health_check():
    return 'GraphQL server is running'

def start_server():
    """启动GraphQL服务器"""
    print("Starting GraphQL server...")
    import uvicorn
    uvicorn.run(app, host='localhost', port=5000)

def stop_server():
    """停止GraphQL服务器"""
    print("Stopping GraphQL server...")
    # 由于FastAPI在单独的线程中运行，我们可以通过设置一个标志来停止它
    # 这里简化处理，实际生产环境中可能需要更复杂的停止机制
    pass

if __name__ == '__main__':
    # 启动服务器
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("GraphQL server started on http://localhost:5000/graphql")
    print("GraphiQL interface available at http://localhost:5000/graphql")
    
    # 运行一段时间
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        stop_server()
        print("Exited")