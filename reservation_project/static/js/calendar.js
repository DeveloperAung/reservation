function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: function(fetchInfo, successCallback) {
            fetch('/events/?start=' + fetchInfo.startStr + '&end=' + fetchInfo.endStr)
                .then(response => response.json())
                .then(events => {
                    let filtered = events.filter(event => {
                        let checkbox = document.querySelector(`input[data-category="${event.category}"]`);
                        return checkbox.checked;
                    });
                    successCallback(filtered);
                });
        },
        editable: true,
        eventDrop: function(info) {
            fetch('/update_event/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    id: info.event.id,
                    start: info.event.start.toISOString(),
                    end: info.event.end ? info.event.end.toISOString() : info.event.start.toISOString()
                })
            }).then(response => {
                if (!response.ok) {
                    info.revert();
                }
            });
        },
        eventClick: function(info) {
            const editUrl = `/edit/${info.event.id}/`;
            const deleteUrl = `/delete/${info.event.id}/`;
            alert(`Event: ${info.event.title}\nDescription: ${info.event.extendedProps.description}\nCategory: ${info.event.extendedProps.category}\n\n[ <a href="${editUrl}">Edit</a> | <a href="${deleteUrl}">Delete</a> ]`);
        },
        eventDidMount: function(info) {
            info.el.style.backgroundColor = info.event.backgroundColor;
            info.el.style.borderColor = info.event.borderColor;
            info.el.classList.add(info.event.extendedProps.category);
        }
    });

    document.querySelectorAll('.filters input').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            calendar.refetchEvents();
        });
    });

    calendar.render();
});