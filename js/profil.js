
var j = jQuery.noConflict();
j(document).ready(function() {
    var calendarEl = document.getElementById('calendar');
    var popupEl; // variable pour stocker la popup actuellement affichée
    var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'fr',
        initialView: 'dayGridMonth',
        events: '/rdv/' + window.location.href.split('/').pop(),
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
        select: function(arg) {
            console.log(arg);
        },
        eventClassNames: function(arg) {
            // Récupération de la date actuelle
            var now = new Date();
            // Vérification si la date de fin de l'événement est antérieure à la date actuelle
            if (arg.event.end < now) {
                // Si l'événement est terminé, on change la couleur en gris
                return ['event-finished'];
            } else {
                // Sinon, on garde la couleur initiale
                return ['event-ongoing'];
            }
        },
        eventClick: function(arg) {
            console.log(arg.event)
            
            // Vérifie si une popup est déjà affichée
            if (popupEl) {
                // Supprime la popup existante
                j(popupEl).dialog("close");
                j(popupEl).remove();
            }
            
            // Récupération des informations de l'événement
            var user = arg.event.extendedProps.user;
            var id = arg.event.extendedProps.id;
            var title = arg.event.title;
            var start = arg.event.start;
            var end = arg.event.end;
            var lieu = arg.event.extendedProps.lieux;
            var name = arg.event.extendedProps.name;
            var eleve = arg.event.extendedProps.eleve;
            var inspecteur = arg.event.extendedProps.inspecteur;
            var heuresPayees = arg.event.extendedProps.heurePayee;
            var heuresRestantes = arg.event.extendedProps.heureRestante;
            // Création de la popup
            var popup = '<div class="popup" style="text-align: center;">';
            popup += '<p class="croix" style="text-align: right; font-size: 20px; cursor: pointer;">&#10006;</p>';
            popup += '<p style="font-size: 20px;"><strong>Title:</strong> ' + name + '</p>';
            popup += '<p><strong>Start:</strong> ' + start.toLocaleString() + '</p>';
            popup += '<p><strong>End:</strong> ' + end.toLocaleString() + '</p>';
            popup += '<p><strong>Lieu:</strong> ' + lieu + '</p>';
            popup += '<p><strong>Eleve:</strong> ' + eleve + '</p>';
            popup += '<p><strong>Inspecteur:</strong> ' + inspecteur + '</p>';
            popup += '<p><strong>Heures payées:</strong> ' + heuresPayees + '</p>';
            popup += '<p><strong>Heures restantes:</strong> ' + heuresRestantes + '</p>';
            if (user == 'secretaire') {
                popup += '<div class="popup" style="display: grid; grid-template-columns: 1fr 1fr; text-align: center;">';
                popup += '<p><a href="/rdv/update/' + arg.event.id + '" class="btn btn-primary">Modifier</a></p>';
                popup += '<p><a href="/rdv/delete/' + arg.event.id + '" class="btn btn-danger">Supprimer</a></p>';
                popup += '</div>';
            }
            popup += '</div>';

            
            // Affichage de la popup
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
                // Supprime la popup lorsqu'on clique dessus
                console.log(user);
                j(this).remove();
                popupEl = null; // Remise à zéro de la variable de la popup affichée
            };
            popupEl.croix.onclick = function() {
                // Supprime la popup lorsqu'on clique sur la croix
                console.log(user);
                j(this).remove();
                popupEl = null; // Remise à zéro de la variable de la popup affichée
            };
            
            // Configuration du popup avec jQuery UI
            j(popupEl).dialog({
                modal: true,
                width: 500,
                height: 400,
                close: function() {
                    // Supprime la popup lorsqu'elle est fermée
                    j(this).remove();
                    popupEl = null; // Remise à zéro de la variable de la popup affichée
                }
            });
        }
    });
    calendar.render();
});