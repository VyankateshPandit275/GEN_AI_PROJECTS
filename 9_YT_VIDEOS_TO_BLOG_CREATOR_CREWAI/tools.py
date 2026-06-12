from crewai_tools import YoutubeChannelSearchTool
from crewai.tools import BaseTool

class YoutubeToolWrapper(BaseTool):
    name: str = "YoutubeChannelSearch"
    description: str = "Search krishnaik06 YouTube channel content for a given topic."

    def _run(self, query: str) -> str:
        import subprocess, sys
        yt = YoutubeChannelSearchTool.__new__(YoutubeChannelSearchTool)
        # Call the underlying search directly, bypassing __init__ URL validation
        from crewai_tools.tools.rag.rag_tool import RagTool
        RagTool.__init__(yt)
        return yt._run(query, youtube_channel_handle='https://www.youtube.com/@krishnaik06')

tool = YoutubeToolWrapper()