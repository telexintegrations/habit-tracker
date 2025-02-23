# Habit Tracker: Telex Integration

Habit Tracker is a [Telex](https://telex.im) integration that sends periodic reminders to log habits in a specified channel. It helps users build consistent routines by prompting them to track their habits daily.

## Key Features
- ⏰ **Interval-Based Reminders**: Schedule reminders using cron syntax (e.g., daily at 9 AM).
- 📝 **Custom Habits**: Define habits as a comma-separated list (e.g., `Exercise, Read`).
- ✅ **Telex Compatibility**: Works seamlessly with Telex channels and settings.

## Setup Instructions

## Prerequisites
- A Telex account and channel.
- The integration JSON hosted on a public URL.

### Installation

1. Clone this repository:

   ```sh
   git clone https://github.com/telex_integrations/habit-tracker.git
   cd habit-tracker
## Setup
1. **Install the Integration**:
   - In your Telex organization, navigate to **Integrations > Add New**.
   - Provide the URL to the [integration JSON file](https://habit-tracker-3aip.onrender.com/integration.json).

2. **Configure Settings**:
   - `interval`: Set the schedule (e.g., Daily for daily reminders).
   - `habits`: List habits to track (e.g., `Exercise, Meditate, Read`).

3. **Enable in Channel**:
   - Add the integration to your desired Telex channel under **Channel Settings > Integrations**.

## How It Works
1. Telex calls the `tick_url` at the configured interval.
2. The integration sends a formatted message to the channel via `return_url`:
