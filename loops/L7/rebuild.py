class Reminder:
    def __init__(self, text):
        self.text = text

    def show_reminder(self, view_reminder):
        self.text = view_reminder
        print(f"1st reminder: {self.text}")

class Alarm(Reminder):
    def __init__(self, text, r_time):
        super().__init__(text)
        self.r_time = r_time

    def show_reminder(self, new_reminder, new_time="At 8pm"):
        super().show_reminder(new_reminder)
        self.new_time = new_time
        print(f"1st reminder: {self.text} at {self.new_time}")


reminder1 = Reminder("Do homework")
alarm1 = Alarm("Help Mom", "At 6pm")

reminder1.show_reminder("Help Mom")
print(reminder1.text)

alarm1.show_reminder("Help Dad")
print(alarm1.text)
print(alarm1.new_time)
