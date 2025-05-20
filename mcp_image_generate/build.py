import os
import PyInstaller.__main__

def build_stdio():
    """Build stdio mode executable"""
    # Ensure dist directory exists
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # Build parameters for stdio mode
    params = [
        'stdio_server.py',
        '--name=image_stdio',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--add-data=.env:.',
        '--hidden-import=image_service'
    ]
    
    # Execute build
    PyInstaller.__main__.run(params)

def build_mcp():
    """Build MCP mode executable"""
    # Ensure dist directory exists
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # Build parameters for MCP mode
    params = [
        'mcp_server.py',
        '--name=image_mcp',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--add-data=.env:.',
        '--hidden-import=image_service',
        '--hidden-import=mcp.server',
        '--hidden-import=mcp.server.stdio',
        '--hidden-import=mcp.server.fastmcp.tools',
        '--hidden-import=anyio',
        '--hidden-import=anyio.streams.memory'
    ]
    
    # Execute build
    PyInstaller.__main__.run(params)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'mcp':
        build_mcp()
    else:
        build_stdio() 