#!/bin/bash

# L-150 Twitter Thread Posting Script
# Usage: ./post-twitter-thread.sh [thread_file]

set -e

THREAD_FILE="${1:-../L-150-TWITTER-THREAD-v4.2.md}"
LOG_FILE="../memory/twitter-posting-$(date +%Y-%m-%d-%H%M).log"

echo "=== L-150 Twitter Thread Posting ===" | tee -a "$LOG_FILE"
echo "Time: $(date)" | tee -a "$LOG_FILE"
echo "Thread file: $THREAD_FILE" | tee -a "$LOG_FILE"

# Check if thread file exists
if [ ! -f "$THREAD_FILE" ]; then
    echo "ERROR: Thread file not found: $THREAD_FILE" | tee -a "$LOG_FILE"
    exit 1
fi

# Extract tweets from thread file
echo "Extracting tweets from thread file..." | tee -a "$LOG_FILE"

# This is a template script - actual Twitter API integration would need to be implemented
# For now, it outputs the tweets that need to be posted

TWEETS=()
CURRENT_TWEET=""
IN_TWEET=false

while IFS= read -r line; do
    if [[ "$line" =~ ^###\ Tweet\ ([0-9]+)/[0-9]+: ]]; then
        if [ -n "$CURRENT_TWEET" ]; then
            TWEETS+=("$CURRENT_TWEET")
        fi
        CURRENT_TWEET=""
        IN_TWEET=true
    elif [ "$IN_TWEET" = true ] && [[ ! "$line" =~ ^# ]] && [[ ! "$line" =~ ^$ ]]; then
        CURRENT_TWEET+="$line"$'\n'
    fi
done < "$THREAD_FILE"

# Add the last tweet
if [ -n "$CURRENT_TWEET" ]; then
    TWEETS+=("$CURRENT_TWEET")
fi

echo "Found ${#TWEETS[@]} tweets to post" | tee -a "$LOG_FILE"

# Display tweets
for i in "${!TWEETS[@]}"; do
    echo "" | tee -a "$LOG_FILE"
    echo "=== Tweet $((i+1)) ===" | tee -a "$LOG_FILE"
    echo "${TWEETS[$i]}" | tee -a "$LOG_FILE"
    echo "Character count: ${#TWEETS[$i]}" | tee -a "$LOG_FILE"
done

echo "" | tee -a "$LOG_FILE"
echo "=== Posting Instructions ===" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "To post this thread manually:" | tee -a "$LOG_FILE"
echo "1. Log in to Twitter/X account" | tee -a "$LOG_FILE"
echo "2. Post Tweet 1 at 9:00 AM SGT" | tee -a "$LOG_FILE"
echo "3. Reply to previous tweet with next tweet every 5-10 minutes" | tee -a "$LOG_FILE"
echo "4. Monitor replies and engage with comments" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "For automated posting, you need to:" | tee -a "$LOG_FILE"
echo "1. Set up Twitter API credentials" | tee -a "$LOG_FILE"
echo "2. Install Twitter API client library" | tee -a "$LOG_FILE"
echo "3. Implement posting logic with rate limiting" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "=== Hashtags to include ===" | tee -a "$LOG_FILE"
echo "#AITreasury #RWATokenization #AIGovernance #PhysicalOracle #DeFi #RealWorldAssets #AIInfrastructure #Web3 #Crypto #Investment #VentureCapital #Startup #Blockchain" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "Script completed at $(date)" | tee -a "$LOG_FILE"

# Make script executable
chmod +x "$0"

echo "" | tee -a "$LOG_FILE"
echo "To run this script: ./$(basename "$0") [thread_file]" | tee -a "$LOG_FILE"