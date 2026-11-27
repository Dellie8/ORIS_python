
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QRadioButton, QCheckBox, QPushButton, QButtonGroup

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Manager")
        self.resize(600, 650)

        self.tasks = []
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        layout.addWidget(QLabel("Task:"))

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter task name...")
        layout.addWidget(self.task_input)

        layout.addWidget(QLabel("Description:"))

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter description...")
        layout.addWidget(self.description_input)
        layout.addWidget(QLabel("Priority:"))

        priority_layout = QHBoxLayout()

        self.low_radio = QRadioButton("Low")
        self.medium_radio = QRadioButton("Medium")
        self.high_radio = QRadioButton("High")

        self.priority_group = QButtonGroup(self)
        self.priority_group.addButton(self.low_radio)
        self.priority_group.addButton(self.medium_radio)
        self.priority_group.addButton(self.high_radio)

        self.medium_radio.setChecked(True)
        priority_layout.addWidget(self.low_radio)
        priority_layout.addWidget(self.medium_radio)
        priority_layout.addWidget(self.high_radio)

        layout.addLayout(priority_layout)

        layout.addWidget(QLabel("Additional settings:"))

        self.important_checkbox = QCheckBox("Important")
        self.notification_checkbox = QCheckBox("Send notification")

        layout.addWidget(self.important_checkbox)
        layout.addWidget(self.notification_checkbox)

        self.create_button = QPushButton("Create task")
        self.clear_button = QPushButton("Clear form")
        self.delete_button = QPushButton("Delete last task")

        layout.addWidget(self.create_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.delete_button)

        self.status_label = QLabel("Status: Ready")
        self.count_label = QLabel("Created tasks: 0")

        layout.addWidget(self.status_label)
        layout.addWidget(self.count_label)

        self.create_button.clicked.connect(self.create_task)
        self.clear_button.clicked.connect(self.clear_form)
        self.delete_button.clicked.connect(self.delete_last_task)

    def create_task(self):
        title = self.task_input.text().strip()
        description = self.description_input.toPlainText()

        if not title:
            self.status_label.setText("Error: Enter task name!")
            return

        priority = self.priority_group.checkedButton().text()

        task = {
            "title": title,
            "description": description,
            "priority": priority,
            "important": self.important_checkbox.isChecked(),
            "notification": self.notification_checkbox.isChecked()
        }

        self.tasks.append(task)

        print("\n--- NEW TASK ---")
        for key, value in task.items():
            print(f"{key}: {value}")

        self.status_label.setText("Status: Task created")
        self.count_label.setText(f"Created tasks: {len(self.tasks)}")

        self.clear_form()

    def clear_form(self):
        self.task_input.clear()
        self.description_input.clear()

        self.medium_radio.setChecked(True)

        self.important_checkbox.setChecked(False)
        self.notification_checkbox.setChecked(False)

        self.status_label.setText("Status: Form cleared")

    def delete_last_task(self):
        if self.tasks:
            self.tasks.pop()
            self.count_label.setText(
                f"Created tasks: {len(self.tasks)}"
            )
            self.status_label.setText("Status: Last task deleted")
        else:
            self.status_label.setText("Status: No tasks to delete")


app = QApplication(sys.argv)

window = TaskManager()
window.show()

sys.exit(app.exec())






