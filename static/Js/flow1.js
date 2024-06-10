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
