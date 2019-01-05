import QtQuick 2.0

Rectangle {
    id: page
    width: 500; height: 200
    color: 'lightblue'

    Text {
        id: hellotext
        text: 'Hello Shane!'
        y: 60
        anchors.horizontalCenter: page.horizontalCenter
        font.pointSize: 24; font.bold: true
    }
}