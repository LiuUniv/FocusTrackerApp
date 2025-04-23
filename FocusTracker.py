import csv
import datetime
import os

import rumps

DEFAULT_DIR = os.path.expanduser("~/Documents/FocusData")

class FocusTrackerApp(rumps.App):
    def __init__(self):
        super().__init__("🎯", title="", quit_button=None)
        self.focusing = False
        self.total_focus_seconds = 0
        self.start_time = None
        self.save_path = DEFAULT_DIR
        self.menu = [
            rumps.MenuItem("开始专注", callback=self.toggle_focus),
            rumps.MenuItem("更换保存目录...", callback=self.set_save_path),
            rumps.MenuItem("今日专注时间: 00:00:00", callback=None),
            None,
            rumps.MenuItem("退出", callback=self.quit_app)
        ]
        rumps.debug_mode(True)
        self.timer = rumps.Timer(self.update_display, 1)
        self.timer.start()

    def toggle_focus(self, sender):
        if not self.focusing:
            self.start_time = datetime.datetime.now()
            sender.title = "结束专注"
            self.focusing = True
        else:
            end_time = datetime.datetime.now()
            delta = (end_time - self.start_time).total_seconds()
            self.total_focus_seconds += delta
            self.log_focus_session(self.start_time, end_time)
            sender.title = "开始专注"
            self.focusing = False

    def update_display(self, _):
        h, rem = divmod(int(self.total_focus_seconds), 3600)
        m, s = divmod(rem, 60)
        self.menu["今日专注时间: 00:00:00"].title = f"今日专注时间: {h:02}:{m:02}:{s:02}"

    def set_save_path(self, _):
        response = rumps.Window(
            title="自定义保存目录",
            message="请输入用于保存专注记录的完整目录路径:",
            default_text=self.save_path,
            dimensions=(400, 20)
        ).run()
        if response.clicked and response.text:
            path = os.path.expanduser(response.text.strip())
            if os.path.isdir(path):
                self.save_path = path
                rumps.notification("设置成功", "", f"保存目录已设置为: {self.save_path}")
            else:
                rumps.alert("该路径不存在, 请确认目录已创建")

    def log_focus_session(self, start, end):
        date_str = start.strftime("%Y-%m-%d")
        filename = f"{self.save_path}/{date_str}.csv"
        os.makedirs(self.save_path, exist_ok=True)
        with open(filename, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([start.strftime("%H:%M:%S"), end.strftime("%H:%M:%S")])

    def quit_app(self, _):
        if self.focusing:
            end_time = datetime.datetime.now()
            delta = (end_time - self.start_time).total_seconds()
            self.total_focus_seconds += delta
            self.log_focus_session(self.start_time, end_time)
        rumps.quit_application()

if __name__ == "__main__":
    FocusTrackerApp().run()
