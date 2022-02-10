import json
import subprocess
import sys
import urllib.request


class GyaoDL:
    def __init__(self, movieid, outputpath):
        try:
            ffmpeg_path = subprocess.check_output(["whereis","ffmpeg"]).split()
            if len(ffmpeg_path) < 2:
                raise
            ffmpeg_path = ffmpeg_path[1]
        except:
            print("FFmpeg is not found")
            sys.exit(1)

        url = 'https://gyao.yahoo.co.jp/apis/playback/graphql'
        params = {
            "appId": "dj00aiZpPUNJeDh2cU1RazU3UCZzPWNvbnN1bWVyc2VjcmV0Jng9NTk-",
            "query": "query Playback($videoId: ID!, $logicaAgent: LogicaAgent!, $clientSpaceId: String!, $os: Os!, "
                     "$device: Device!) { content( parameter: { contentId: $videoId logicaAgent: $logicaAgent "
                     "clientSpaceId: $clientSpaceId os: $os device: $device view: WEB } ) { tracking { streamLog "
                     "vrLog stLog } inStreamAd { forcePlayback source { __typename ... on YjAds { ads { location time "
                     "adRequests { __typename ... on YjAdOnePfWeb { adDs placementCategoryId } ... on "
                     "YjAdOnePfProgrammaticWeb { adDs } ... on YjAdAmobee { url } ... on YjAdGam { url } } } } ... on "
                     "Vmap { url } ... on CatchupVmap { url siteId } } } video { id title delivery { id drm } "
                     "duration images { url width height } cpId playableAge maxPixel embeddingPermission "
                     "playableAgents gyaoUrl } } } ",
            "variables": '{"videoId":"' + movieid + '","logicaAgent":"PC_WEB","clientSpaceId":"1183050133",'
                                                    '"os":"UNKNOWN","device":"PC"} '
        }
        req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
        with urllib.request.urlopen(req) as res:
            graphql = json.loads(res.read())
        url = f'https://edge.api.brightcove.com/playback/v1/accounts/4235717419001/videos/{graphql["data"]["content"]["video"]["delivery"]["id"]}'
        req = urllib.request.Request(url, headers={
            "Accept": "application/json;pk=BCpkADawqM1O4pwi3SZ75b8DE1c2l78PZ418NByBa33h737rWv6uhPJHYkaZ6xHINTj5oOqa0"
                      "-zarOEvQ6e1EqKhBcCppkAUWuo5QSKWVC4HZjY2z-Lo_ptwEK3hxfKuvZXkdNuyOM5nNSWy"})
        with urllib.request.urlopen(req) as res:
            brightcove = json.loads(res.read())
        hlsurl = ""
        for stream in brightcove["sources"]:
            if stream["ext_x_version"] == "4" and stream["type"] == "application/x-mpegURL":
                hlsurl = stream["src"]
                break
            if stream["ext_x_version"] == "5":
                print("This movie is drm enabled")
                sys.exit(2)
        if hlsurl == "":
            print("Active stream is not found")
            sys.exit(1)
        code = subprocess.call(
            [ffmpeg_path, "-i", hlsurl, "-movflags", "faststart", "-c", "copy", "-bsf:a", "aac_adtstoasc", "-loglevel", "error",
             outputpath])
        if code != 0:
            print(f"FFmpeg failed with code {code}")
