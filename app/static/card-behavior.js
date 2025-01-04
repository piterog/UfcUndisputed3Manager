document.addEventListener('DOMContentLoaded', function () {
    const sortableContainer = document.getElementById('sortable-container');

    function toggleBeltOpacity(beltElement) {
        const sortableItem = beltElement.closest('.sortable-item');

        if (beltElement.style.opacity === '1') {
            beltElement.style.opacity = '0.1';
            updateHiddenField(sortableItem, false);
        } else {
            beltElement.style.opacity = '1';
            updateHiddenField(sortableItem, true);
        }
    }

    function updateHiddenField(sortableItem, value) {
        let hiddenField = sortableItem.querySelector('input[name="belt[]"]');
        hiddenField.value = value;
    }

    function addBeltEvent(beltElement) {
        beltElement.addEventListener('click', function () {
            toggleBeltOpacity(beltElement);
        });
    }
    window.addBeltEvent = addBeltEvent;

    const belts = sortableContainer.querySelectorAll('.belt img');
    belts.forEach(addBeltEvent);

    function updateControlField(sortableItem, value) {
        const controlField = sortableItem.querySelector('input[name="control[]"]');
        if (controlField) {
            controlField.value = value;
        }
    }

    function toggleGloveSelection(gloveElement, gloveType) {
        const sortableItem = gloveElement.closest('.sortable-item');
        const redGlove = sortableItem.querySelector('.red-glove img');
        const blueGlove = sortableItem.querySelector('.blue-glove img');
        const controlField = sortableItem.querySelector('input[name="control[]"]');

        if (gloveType === 'red') {
            if (redGlove.src.includes('red-selected.svg')) {
                redGlove.src = "../static/default.svg";
                redGlove.style.opacity = '0.1';
                updateControlField(sortableItem, 0);
            } else {
                redGlove.src = "../static/red-selected.svg";
                blueGlove.src = "../static/default.svg";
                redGlove.style.opacity = '1';
                blueGlove.style.opacity = '0.1';
                updateControlField(sortableItem, 1);
            }
        } else if (gloveType === 'blue') {
            if (blueGlove.src.includes('blue-selected.svg')) {
                blueGlove.src = "../static/default.svg";
                blueGlove.style.opacity = '0.1';
                updateControlField(sortableItem, 0);
            } else {
                blueGlove.src = "../static/blue-selected.svg";
                redGlove.src = "../static/default.svg";
                redGlove.style.opacity = '0.1';
                blueGlove.style.opacity = '1';
                updateControlField(sortableItem, 2);
            }
        }
    }

    function addGloveEvent(gloveElement, gloveType) {
        gloveElement.addEventListener('click', function () {
            toggleGloveSelection(gloveElement, gloveType);
        });
    }
    window.addGloveEvent = addGloveEvent

    const redGloves = sortableContainer.querySelectorAll('.red-glove img');
    const blueGloves = sortableContainer.querySelectorAll('.blue-glove img');

    redGloves.forEach(redGlove => addGloveEvent(redGlove, 'red'));
    blueGloves.forEach(blueGlove => addGloveEvent(blueGlove, 'blue'));

    const initialItems = document.querySelectorAll('.sortable-item');

    initialItems.forEach(item => {
        // Configurar gloves com base em "data-control"
        const control = parseInt(item.dataset.control, 10);
        const redGlove = item.querySelector('.red-glove img');
        const blueGlove = item.querySelector('.blue-glove img');

        if (redGlove && blueGlove) {
            if (control === 1) {
                redGlove.src = "../static/red-selected.svg";
                blueGlove.src = "../static/default.svg";
                redGlove.style.opacity = '1';
                blueGlove.style.opacity = '0.1';
            } else if (control === 2) {
                blueGlove.src = "../static/blue-selected.svg";
                redGlove.src = "../static/default.svg";
                redGlove.style.opacity = '0.1';
                blueGlove.style.opacity = '1';
            } else {
                blueGlove.src = "../static/default.svg";
                redGlove.src = "../static/default.svg";
                redGlove.style.opacity = '0.1';
                blueGlove.style.opacity = '0.1';
            }
        }

        const belt = item.querySelector('.belt img');
        const beltDispute = item.querySelector('.belt img').dataset.beltDispute === 'True';

        if (belt) {
            if (beltDispute) {
                belt.style.opacity = '1';
            } else {
                belt.style.opacity = '0.1';
            }
        }
    });
});