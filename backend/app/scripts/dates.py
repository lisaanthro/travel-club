from datetime import datetime

start_date = datetime(2024, 5, 14, 10, 30, 0)
end_date = datetime(2024, 5, 20, 10, 30, 0)
price = 200
diff = ((end_date - start_date).days + 1) * price

print(diff, (end_date - start_date).days + 1)
