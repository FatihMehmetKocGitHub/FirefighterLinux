import QtQuick 2.0;

Presentation {
    id: presentation

    Slide {
        Image {
            id: background
            source: "/usr/share/backgrounds/firefighterlinux/wallpaper.png"
            anchors.fill: parent
            fillMode: Image.PreserveAspectCrop
        }

        Rectangle {
            anchors.fill: parent
            color: "#000000"
            opacity: 0.35
        }

        Text {
            text: "Firefighter Linux V1.0"
            color: "white"
            font.pixelSize: 42
            font.bold: true
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            text: "Offline-first Disaster Response System"
            color: "#ff4444"
            font.pixelSize: 22
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.verticalCenter
            anchors.topMargin: 55
        }
    }
}
