// ======= Dark Mode JS =========
let datkBtn = document.getElementById('dark-button');
datkBtn.addEventListener('click', function () {
    document.getElementById('body').classList.toggle('dark-mode');
});


// ======= Counter JS =======
$('.counter-value').each(function () {
    var $this = $(this),
        countTo = $this.attr('data-count');
    $({
        countNum: $this.text()
    }).animate({
        countNum: countTo
    },

        {
            duration: 2000,
            easing: 'swing',
            step: function () {
                $this.text(Math.floor(this.countNum));
            },
            complete: function () {
                $this.text(this.countNum);
                //alert('finished');
            }

        });
});
