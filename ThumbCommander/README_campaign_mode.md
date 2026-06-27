# ThumbCommander Campaign Mode

This document explains how to use the campaign mode in ThumbCommander and add own campaigns.

## Implementation Steps

Campaigns are stored in JSON files in the ThumbCommander directory.
To remove campaigns, simply delete the respective JSON file.
Create campaign JSON files with your missions and stories. Only file in the format '*_campaign.json' are picked up!

## Campaign JSON Structure

Campaigns are defined using JSON files in the following format:

```json
{
  "title": "Campaign Title",
  "description": "Short description for selection screen",
  "intro": "Long introduction text shown at the start of the campaign",
  "outro": "Text shown upon campaign completion",
  "missions": [
    {
      "name": "Mission Name",
      "briefing": "Text shown before the mission",
      "debriefing": "Text shown after completing the mission",
      "config": {
        "type": "dogfight|asteroids|mixed",
        "enemies": 1,
        "asteroids": 10,
        "difficulty": 1
      }
    },
    // More missions...
  ]
}
```

### Mission Configuration Options

- `type`: Determines the mission type
  - `dogfight`: Only enemy ships
  - `asteroids`: Only asteroids
  - `mixed`: Both enemies and asteroids
- `enemies`: Number of enemy ships (for dogfight and mixed types)
- `asteroids`: Number of asteroids (for asteroids and mixed types)
- `difficulty`: Value from 1-4 that affects enemy health, speed, and number of objects

### Mission Completion Mechanics

In campaign mode, missions now have a two-phase completion process:

1. **Objective Phase**: Player must complete all specified objectives (time and/or kills)
2. **Cleanup Phase**: After objectives are met, no new enemies or asteroids will spawn, but the player must eliminate all remaining enemies and asteroids to complete the mission. During this cleanup phase, a "CLEAR ALL!" message appears to indicate that the player should destroy all remaining enemies and asteroids.

If the player dies at any point before completing both phases, the mission fails and must be restarted (with a limited number of attempts).

In non-campaign mode (regular gameplay), the original endless gameplay mechanics remain unchanged.

## How to Create a Campaign

1. Create a JSON file with the structure shown above
2. Name it something descriptive ending with `_campaign.json` (e.g., `tc1_campaign.json`)
3. Save it in your ThumbCommander directory

**Campaign Order**: Campaigns are displayed in alphabetical order based on their filenames. To control the display order, use filename prefixes like `01_campaign.json`, `02_campaign.json`, etc.

### Campaign Progression and Saving

The game automatically saves progress after each mission. Players can:
- Continue from their last mission
- Start a new campaign
- Save and exit after a mission

## Available Campaign Files

Four sample campaigns are included:
1. 'astroid_campaign.json' - A pure Astroid Dash Campaign.
2. 'tc1_campaign.json' - Some fun mix between astroid fields, dog fights and both together to show the capabilites of the engine
1. `tc2_campaign.json` - Thumb Commander Legacy: Vega Campaign - To dive back into the 90s
2. `tc3_campaign.json` - Thumb Commander Legacy II: Vengeance - dive back again and enjoy the sequel

## More to come

The Campaign Engine will be further extended in the future:
1. Multi battles per mission
2. Adding new mission types
3. Modifying the difficulty scaling
4. Adding special mission objectives

## Troubleshooting

If you encounter issues:
- Ensure campaign JSON files are correctly formatted
- Check that the files are in the correct directory
- The Thumby has limited memory. Extensive text in the campaign files will quickly bring him to OutOfMemory Exeception!
