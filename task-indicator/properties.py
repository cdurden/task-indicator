# encoding=utf-8

import gtk


class Dialog(gtk.Window):
    def __init__(self, callback=None, debug=False):
        super(gtk.Window, self).__init__()
        self.connect("delete_event", self.on_delete_event)

        self.debug = debug
        self.task = None
        self.callback = callback

        self.set_border_width(10)

        self.grid = gtk.Table(5, 2)
        self.add(self.grid)

        self.description = gtk.Entry()
        self.grid.attach(self.description, 1, 2, 0, 1,
            yoptions=gtk.FILL, xpadding=2, ypadding=2)
        self.grid.attach(gtk.Label("Description:"), 0, 1, 0, 1,
            xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=2, ypadding=2)

        self.project = gtk.Entry()
        self.grid.attach(self.project, 1, 2, 1, 2,
            yoptions=gtk.FILL, xpadding=2, ypadding=2)
        self.grid.attach(gtk.Label("Project:"), 0, 1, 1, 2,
            xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=2, ypadding=2)

        self.tags = gtk.Entry()
        self.grid.attach(self.tags, 1, 2, 2, 3,
            yoptions=gtk.FILL, xpadding=2, ypadding=2)
        self.grid.attach(gtk.Label("Tags:"), 0, 1, 2, 3,
            xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=2, ypadding=2)

        self.completed = gtk.CheckButton("completed")
        self.grid.attach(self.completed, 1, 2, 3, 4,
            yoptions=gtk.FILL, xpadding=2, ypadding=2)

        self.bbx = gtk.HButtonBox()
        self.grid.attach(self.bbx, 0, 2, 4, 5,
            yoptions=gtk.FILL, xpadding=2, ypadding=2)

        self.start = gtk.Button("Start")
        self.start.connect("clicked", self.on_start_stop)
        self.bbx.add(self.start)

        self.close = gtk.Button("Close")
        self.close.connect("clicked", self.on_close)
        self.bbx.add(self.close)

        self.set_title("Task properties")
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_default_size(600, 100)

    def show_task(self, task):
        print "Showing task %s ..." % task["uuid"]

        self.task = task
        self.description.set_text(task["description"])
        self.project.set_text(task["project"])
        self.tags.set_text(", ".join(task["tags"]))

        self.completed.set_active(task["status"] == "completed")

        if "start" in task:
            self.start.set_label("Stop")
        else:
            self.start.set_label("Start")

        self.show_all()
        self.description.grab_focus()

    def on_close(self, widget):
        self.hide()

        if self.callback:
            update = {"uuid": self.task["uuid"]}

            tmp = self.description.get_text()
            if tmp != self.task["description"]:
                update["description"] = tmp

            tmp = self.project.get_text()
            if tmp != self.task["project"]:
                update["project"] = tmp

            tmp = "completed" if self.completed.get_active() else "pending"
            if tmp != self.task["status"]:
                update["status"] = tmp

            self.callback(update)

        if self.debug:
            gtk.main_quit()

    def on_delete_event(self, widget, event, data=None):
        self.on_close(widget)
        return True

    def on_start_stop(self, widget):
        if "start" in self.task:
            self.on_task_stop(self.task)
        else:
            self.on_task_start(self.task)
        self.on_close(widget)

    def on_task_start(self, task):
        print "task %s start" % self.task["uuid"]

    def on_task_stop(self, task):
        print "task %s stop" % self.task["uuid"]


def main():
    def take2(task):
        if len(task) > 1:
            print "Task update:", task

    w = Dialog(callback=take2, debug=True)
    w.show_task({"uuid": "2ea544b9-a068-4e3e-a99d-5235ed53a17f",
            "description": "Hello, world.",
            "project": "oss.taskwarrior",
            "tags": "hobby, linux",
            "start": "20130203T163010Z",
            "status": "completed"})
    gtk.main()


if __name__ == "__main__":
    main()
