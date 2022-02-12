# BUILDING

Building requires python3.10, and the build package, which can be installed via pip:
```bash
python3.10 -m pip install build
```

To install, run 
```bash
python3.10 -m pip install -r requirements.txt
python3.10 -m pip install dist/yt_feed-*.whl 
```


Now, add a channel via 
```bash
feed --add <channel-id>
```
where channel-id is for instance :
UCX6OQ3DkcsbYNE6H8uQQuVA of https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA