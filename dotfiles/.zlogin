cat /etc/motd
date +"It's %I:%M%P on %A, %B %d, in week %W of year %Y."
echo
echo "This server has been `uptime -p`."
echo
df -h | grep -E '(/mnt/sd|/home|Used Avail)'
echo
who
echo
