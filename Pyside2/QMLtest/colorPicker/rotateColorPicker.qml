import QtQuick 2.0

Rectangle {
    id: page
    width: 500; height: 300
    color: 'lightgray'

    Text {
        id: hellotext
        text: 'Hello Shane!'
        y: 50
        anchors.horizontalCenter: page.horizontalCenter
        font.pointSize: 40; font.bold: true

        MouseArea {
            id: mouseArea
            anchors.fill: parent
        }

        states: State {
            name: 'down'; when: mouseArea.press == true
            PropertyChanges { target: hellotext; y: 160; rotation: 180; color: 'red'}
        }

        transitions : Transition {
            from: ''; to: 'down'; reversible: true
            ParallelAnimation {
                NumberAnimation { properties: 'y,rotation'; duration: 500; easing.type: Easing.InOutQuad }
                ColorAnimation { duration: 500 }
            }
        }
    }

    Grid {
        id: colorPicker
        x: 8; anchors.bottom: page.bottom; anchors.bottomMargin: 4
        rows: 2; columns: 3; spacing: 5

        Pickcolor { cellColor: 'red'; onClicked: hellotext.color = cellColor }
        Pickcolor { cellColor: 'green'; onClicked: hellotext.color = cellColor }
        Pickcolor { cellColor: 'blue'; onClicked: hellotext.color = cellColor }
        Pickcolor { cellColor: 'yellow'; onClicked: hellotext.color = cellColor }
        Pickcolor { cellColor: 'steelblue'; onClicked: hellotext.color = cellColor }
        Pickcolor { cellColor: 'black'; onClicked: hellotext.color = cellColor }
    }
}