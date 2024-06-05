!/bin/bash

LIMIT_DAYS=30

cur_date=$(date +%s)

users=$(awk -F: '$3 >= 1000 {print $1}' /etc/passwd)

for user in $users; do
	
	l_login=$(lastlog -u "$user" | awk 'NR==2 {print $4, $5, $6}')
	l_log_date=$(date -d "$l_login" +%s 2>/dev/null)
	
	if [ -n "$l_log_date" ] && [ "$l_log_date" -le "$cur_date" ]; then
		dif_day=$((cur_date - l_log_date) / 86400))
		
		if [ "$dif_day" -gt "$LIMIT_DAYS" ]; then
			echo "ВИдаляю користувача $user"
			sudo userdel -r "$user"
		fi
	fi
done