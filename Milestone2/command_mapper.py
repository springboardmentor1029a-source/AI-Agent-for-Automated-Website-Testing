def map_to_command(parsed_instruction):
    commands = []

    if parsed_instruction["action"] == "open_url":
        commands.append({
            "command": "OPEN_BROWSER",
            "target": parsed_instruction["url"]
        })

    if parsed_instruction["assert"] == "title_contains":
        commands.append({
            "command": "ASSERT_TITLE",
            "value": parsed_instruction["value"]
        })

    return commands
