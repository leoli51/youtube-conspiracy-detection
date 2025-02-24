import srt


def text_from_subtitles(raw_subtitles: str) -> str:
	subs = []
	for sub in srt.parse(raw_subtitles):
		for s in sub.content.splitlines():
			subs.append(s.strip())
	# Handle case where subs are present but empty
	if not subs:
		return ""
	pretty_subs = [subs[0]]
	last_pretty_sub = subs[0]
	for sub in subs:
		if sub in ["\n", "", " ", last_pretty_sub]:
			continue
		else:
			pretty_sub = sub.replace(last_pretty_sub, "")
			pretty_subs.append(pretty_sub)
			last_pretty_sub = pretty_sub

	return "\n".join(pretty_subs)
