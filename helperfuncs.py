
def getClips(loc, scale, clip_value_bottom, clip_value_top):
    clip_a = (clip_value_bottom - loc) / scale
    clip_b = (clip_value_top - loc) / scale

    clips = {
        'a': clip_a,
        'b': clip_b
    }

    return clips
