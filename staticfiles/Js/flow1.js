document.addEventListener('DOMContentLoaded', function() {
  const formSteps = document.querySelectorAll('.form-step');
  const steps = document.querySelectorAll('.step');
  let currentStep = 0;

  formSteps[currentStep].classList.add('active');
  steps[currentStep].classList.add('active');

  window.nextStep = (step) => {
    if (validateStep(step - 1)) {
      formSteps[step - 1].classList.remove('active');
      steps[step - 1].classList.remove('active');
      steps[step - 1].classList.add('completed');
      
      currentStep = step;
      
      formSteps[currentStep].classList.add('active');
      steps[currentStep].classList.add('active');
    }
  };

  window.previousStep = (step) => {
    formSteps[step].classList.remove('active');
    steps[step].classList.remove('active');
    steps[step].classList.remove('completed');
    
    currentStep = step - 1;
    
    formSteps[currentStep].classList.add('active');
    steps[currentStep].classList.add('active');
  };

  function validateStep(step) {
    const formElements = formSteps[step].querySelectorAll('input, select, textarea');
    let isValid = true;

    formElements.forEach(input => {
      const errorTag = input.nextElementSibling;
      if (!input.checkValidity()) {
        isValid = false;
        input.classList.add('input-error');
        if (errorTag) { 
          errorTag.innerText = `${capitalize(input.name)} is required`;
        }
      } else {
        input.classList.remove('input-error');
        if (errorTag) { 
          errorTag.innerText = '';
        }
      }
    });

    return isValid;
  }

  function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  document.getElementById('signupForm').addEventListener('submit', function(event) {
    if (!validateStep(currentStep)) {
      event.preventDefault(); // Prevent form submission if current step is invalid
    }
  });
});
      const specificDateCheckbox = document.getElementById('specificDate');
      const specificDateContainer = document.getElementById('specificDateContainer');
      const asapCheckbox = document.getElementById('asap');
      const flexibleCheckbox = document.getElementById('flexible');
      // const termsCheckbox = document.getElementById('terms');
      // const termsError = document.getElementById('termsError'); 
  
      // Initially hide the specific date container
      specificDateContainer.style.display = 'none';
  
      specificDateCheckbox.addEventListener('change', function() {
          if (this.checked) {
              specificDateContainer.style.display = 'block';
              // Uncheck other checkboxes
              asapCheckbox.checked = false;
              flexibleCheckbox.checked = false;
          } else {
              specificDateContainer.style.display = 'none';
          }
      });
  
      // Listen to change event on other checkboxes to manage unchecking
      asapCheckbox.addEventListener('change', function() {
          if (this.checked) {
              specificDateContainer.style.display = 'none';
              // Uncheck specificDate if asap is checked
              specificDateCheckbox.checked = false;
              flexibleCheckbox.checked = false;
          }
      });
  
      flexibleCheckbox.addEventListener('change', function() {
          if (this.checked) {
              specificDateContainer.style.display = 'none';
              // Uncheck specificDate if flexible is checked
              specificDateCheckbox.checked = false;
              asapCheckbox.checked = false;
          }
      });
  
      // Validate passwords
      
  
      // Validate terms checkbox
      // function validateTerms() {
      //     if (!termsCheckbox.checked) {
      //         termsError.innerText = 'You must agree to the terms and conditions';
      //         return false;
      //     } else {
      //         termsError.innerText = ''; // Clear error message
      //         return true;
      //     }
      // }
  
      // Handle form submission
      // document.getElementById('signupForm').addEventListener('submit', function(event) {
      //     if (!validateTerms()) {
      //         event.preventDefault(); // Prevent form submission if validation fails
      //     }
      // });
  