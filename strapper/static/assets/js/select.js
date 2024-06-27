var selectedJobs={};
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {
    const customSelects = document.querySelectorAll(".custom-select");

    function updateSelectedOption(customSelect) {
        const selectedOption = Array.from(customSelect.querySelectorAll('.option.active'))
            .filter(option => option !== customSelect.querySelector(".option.all-tags"))
            .map((option) => {
                return {
                    value: option.getAttribute('data-value'),
                    text: option.textContent.trim()
                };
            });
        console.log("update in array...", selectedOption);
        selectedJobs = selectedOption;
        const selectedValues = selectedOption.map((option) => option.value);
        customSelect.querySelector(".tag_input").value = selectedValues.join(", ");
        let tagHTML = "";
        if (selectedOption.length === 0) {
            tagHTML = '<span class="placeholder">Select the jobs</span>';
        } else {
            const maxTagToShow = 100;
            let additionalTagCount = 0;
            selectedOption.forEach((option, index) => {
                if (index < maxTagToShow) {
                    tagHTML += "<span class='tag'>" + option.text +
                        '<span class="remove-tag" data-value="' + option.value + '">&times;</span></span>';
                } else {
                    additionalTagCount++;
                }
            });
            if (additionalTagCount > 0) {
                tagHTML += '<span class="tag">+' + additionalTagCount + '</span>';
            }
        }
        customSelect.querySelector('.selected-options').innerHTML = tagHTML;
    }

    customSelects.forEach((customSelect) => {
        const searchInput = customSelect.querySelector(".search-tags");
        const optionsContainer = customSelect.querySelector(".options");
        const noResultMessage = customSelect.querySelector('.no-result-message');
        const options = customSelect.querySelectorAll(".option");
        const allTagsOption = customSelect.querySelector(".option.all-tags");
        const clearButton = customSelect.querySelector(".clear");

        allTagsOption.addEventListener('click', () => {
            const isActive = allTagsOption.classList.contains('active');
            options.forEach((option) => {
                if (option !== allTagsOption) {
                    option.classList.toggle("active", !isActive);
                }
            });
            updateSelectedOption(customSelect);
        });

        clearButton.addEventListener('click', () => {
            searchInput.value = "";
            options.forEach((option) => {
                option.style.display = "block";
            });
            noResultMessage.style.display = "none";
        });

        searchInput.addEventListener("input", () => {
            const searchTerm = searchInput.value.toLowerCase();
            options.forEach((option) => {
                const optionText = option.textContent.trim().toLowerCase();
                const shouldShow = optionText.includes(searchTerm);
                option.style.display = shouldShow ? "block" : "none";
            });
            const visibleOptions = Array.from(options).some(option => option.style.display === "block");
            noResultMessage.style.display = visibleOptions ? "none" : "block";
            if (searchInput.value) {
                optionsContainer.classList.add('option-search-active');
            } else {
                optionsContainer.classList.remove('option-search-active');
            }
        });
    });

    customSelects.forEach((customSelect) => {
        const options = customSelect.querySelectorAll(".option");
        options.forEach((option) => {
            option.addEventListener('click', () => {
                option.classList.toggle('active');
                updateSelectedOption(customSelect);
            });
        });
    });

    document.addEventListener('click', (eve) => {
        const removeTag = eve.target.closest(".remove-tag");
        if (removeTag) {
            const customSelect = removeTag.closest(".custom-select");
            const valueToRemove = removeTag.getAttribute("data-value");
            const optionToRemove = customSelect.querySelector(".option[data-value='" + valueToRemove + "']");
            optionToRemove.classList.remove("active");
            const otherSelectedOption = customSelect.querySelectorAll(".option.active:not(.all-tags)");
            const allTagsOption = customSelect.querySelector(".option.all-tags");
            if (otherSelectedOption.length === 0) {
                allTagsOption.classList.remove("active");
            }
            updateSelectedOption(customSelect);
        }
    });

    const selectBoxes = document.querySelectorAll(".select-box");
    selectBoxes.forEach((selectBox) => {
        selectBox.addEventListener("click", (eve) => {
            if (eve.target.closest(".tag")) {
                selectBox.parentNode.classList.toggle("open");
            }
        });
    });

    document.addEventListener("click", (eve) => {
        if (!eve.target.closest(".custom-select") || eve.target.classList.contains("remove-tag")) {
            customSelects.forEach((customSelect) => {
                customSelect.classList.remove("open");
            });
        }else{
            customSelects.forEach((customSelect) => {
                customSelect.classList.add("open");
            });
        }
    });


    function resetCustomSelect() {
        customSelects.forEach((customSelect) => {
            customSelect.querySelectorAll(".option.active").forEach((option) => {
                option.classList.remove("active");
            });
            customSelect.querySelector(".option.all-tags").classList.remove("active");
            updateSelectedOption(customSelect);
        });
    }

    // Ensure initial state is correctly set
    customSelects.forEach(customSelect => updateSelectedOption(customSelect));
    resetCustomSelect();
    document.getElementById("button").addEventListener('click',(eve)=>{
    
    const url = '/select_job/';
    const jsonData = JSON.stringify(selectedJobs);
    console.log("button clicked...",csrftoken,jsonData)
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: jsonData
    };
    fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('POST request successful:', data);
            if(data.result !== null){
                console.log("Redirecting....")
                window.location.href=data.result
            }  
        })
        .catch(error => {
            console.error('Error sending POST request:', error);
    });
})
});

