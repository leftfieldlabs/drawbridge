var Drawbridge = function() {

    this.howItWorksSection = document.querySelector('.how-it-works');
    this.howItWorksOffset = this.howItWorksSection.offsetTop - 300;

    this.drawbridgeGif = document.querySelector('.diagram-drawbridge');
    this.drawbridgePlaceholder = document.querySelector('.diagram-drawbridge-placeholder');
    this.init();
};

Drawbridge.prototype.init = function() {

    document.addEventListener('scroll', function(e) {
        if(window.pageYOffset >= this.howItWorksOffset) {
            this.drawbridgePlaceholder.classList.add('hide');
            this.drawbridgeGif.classList.add('active');
        }
    }.bind(this));
};
