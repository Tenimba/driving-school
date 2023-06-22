$(function() {
    $('.timepicker').timepicker({
        timeFormat: 'HH:mm',
        interval: 15,
        minTime: '00:00',
        maxTime: '23:45',
        startTime: '00:00',
        dynamic: false,
        dropdown: true,
        scrollbar: true
    });
});
