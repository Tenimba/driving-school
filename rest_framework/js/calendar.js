
var j = jQuery.noConflict();
j(document).ready(function() {
    var calendarEl = document.getElementById('calendar');
    var popupEl = null;
    
    var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'fr',
        timeZone: 'UTC',
        initialView: 'dayGridMonth', 
        events: '/rdv_json/',
        eventColor: '#378006',
        eventTextColor: 'white',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
        },
        navLinks: true,
        editable: false,
        dayMaxEvents: true,
        selectable: true,
        selectMirror: true,
        eventClassNames: function(arg) {
            var now = new Date();
            if (arg.event.end < now) {
                return ['event-finished'];
            } else {
                return ['event-ongoing'];
            }
        },
        eventClick: function(arg) {
            if (popupEl) {
                j(popupEl).dialog("close");
                j(popupEl).remove();
            }
            var user = arg.event.extendedProps.user;
            var id = arg.event.id;
            var title = arg.event.title;
            var start = arg.event.start.toUTCString();
            var end = arg.event.end.toUTCString();
            var lieu = arg.event.extendedProps.lieux;
            var name = arg.event.extendedProps.name;
            var eleve = arg.event.extendedProps.eleve;
            var inspecteur = arg.event.extendedProps.inspecteur;
            var heuresPayees = arg.event.extendedProps.heurePayee;
            var heuresRestantes = arg.event.extendedProps.heureRestante;

            var popup = '<div class="popup" style="text-align: center;">';
            popup += '<p class="croix" style="text-align: right; font-size: 20px; cursor: pointer;">&#10006;</p>';
            popup += '<p style="font-size: 20px;"><strong>Title:</strong> ' + name + '</p>';
            popup += '<p><strong>Start:</strong> ' + start+ '</p>';
            popup += '<p><strong>End:</strong> ' + end + '</p>';
            popup += '<p><strong>Lieu:</strong> ' + lieu + '</p>';
            popup += '<p><strong>Eleve:</strong> ' + eleve + '</p>';
            popup += '<p><strong>Inspecteur:</strong> ' + inspecteur + '</p>';
            popup += '<p><strong>Heures payées:</strong> ' + heuresPayees + '</p>';
            popup += '<p><strong>Heures restantes:</strong> ' + heuresRestantes + '</p>';
            if (user == 'secretaire' || user == 'inspecteur') {
                popup += '<div class="popup" style="display: grid; grid-template-columns: 1fr 1fr; text-align: center;">';
                popup += '<p><a href="/rdv/update/' + arg.event.id + '" class="btn btn-primary">Modifier</a></p>';
                popup += '<p><a href="/rdv/delete/' + arg.event.id + '" class="btn btn-danger">Supprimer</a></p>';
                popup += '</div>';
            }
            popup += '</div>';

            popupEl = document.createElement('div');
            popupEl.setAttribute('id', 'popup');
            popupEl.setAttribute('title', 'Event details');
            popupEl.innerHTML = popup;
            document.body.appendChild(popupEl);
            popupEl.style.backgroundColor = '#f9f9f9';
            popupEl.style.border = '1px solid #eaeaea';
            popupEl.style.borderRadius = '5px';
            popupEl.style.padding = '10px';
            popupEl.style.marginTop = '10px';
            popupEl.style.marginBottom = '10px';
            popupEl.style.display = 'inline-block';
            popupEl.style.position = 'absolute';
            popupEl.style.top = '50%';
            popupEl.style.left = '50%';
            popupEl.style.transform = 'translate(-50%, -50%)';
            popupEl.style.zIndex = '1000';
            popupEl.onclick = function() {
                j(this).remove();
                popupEl = null;
            };
            popupEl.croix.onclick = function() {
                j(this).remove();
                popupEl = null;
            };

            j(popupEl).dialog({
                modal: true,
                width: 500,
                height: 400,
                close: function() {
                    j(this).remove();
                    popupEl = null;
                }
            });
        }
    });
    calendar.render();
    
$('.car').css({left: $(window).width(), top: 0});

function moveCar(event) {
  $('.car').css({left: event.pageX, top: event.pageY});
}

setInterval(function() {
  if ($('.car').hasClass('move')) {
    var carPosition = $('.car').position().left;
    if (carPosition < -200) {
      $('.car').css({left: $(window).width(), top: 0});
    } else {
      moveCar({
        pageX: $('.car').position().left - 5,
        pageY: $('.car').position().right
      });
    }
  }
}, 50);

$('html').on('mousemove', function(event) {
  $('.car').addClass('move');
});

$('html').on('mouseleave', function() {
  $('.car').removeClass('move');
});

});