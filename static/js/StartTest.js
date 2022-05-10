function myfunction() {
    $('a#test').bind('click', function() {
        $.post('/InterfaceTestAssemblage',
            function(data) {

            });
        return false;
    });
};

function Refresh() {
    window.parent.location = window.parent.location.href;
}