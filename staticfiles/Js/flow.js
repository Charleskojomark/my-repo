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
      formSteps[step].classList.remove
      ('active');
      steps[step].classList.remove('active');
      steps[step].classList.remove('completed');
      
      currentStep = step - 1;
      
      formSteps[currentStep].classList.add('active');
      steps[currentStep].classList.add('active');
    };
  
    function validateStep(step) {
      const form = formSteps[step].querySelectorAll('input, select, textarea');
      let isValid = true;
      
      form.forEach(input => {
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
      
      // if (step === 4) {
      //   const password = formSteps[4].querySelector('#password');
      //   const confirmPassword = formSteps[4].querySelector('#confirmPassword');
      //   const confirmPasswordError = confirmPassword.nextElementSibling;
      
      //   if (password.value !== confirmPassword.value) {
      //     isValid = false;
      //     password.classList.add('input-error');
      //     confirmPassword.classList.add('input-error');
      //     confirmPasswordError.innerText = 'Passwords do not match';
      //   } else {
      //     password.classList.remove('input-error');
      //     confirmPassword.classList.remove('input-error');
      //     confirmPasswordError.innerText = '';
      //   }
      // }
      return isValid;
    }
    function capitalize(str) {
      return str.charAt(0).toUpperCase() + str.slice(1);
    }
  
    function validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(String(email).toLowerCase());
    }
  
    
  
    
  
    
  
    function capitalize(str) {
      return str.charAt(0).toUpperCase() + str.slice(1);
    }

    

    // const specificDateInput = document.getElementById('specificDate');
    // const specificDateContainer = document.getElementById('specificDateContainer');

    // // Initially hide the specific date container
    // specificDateContainer.style.display = 'none';

    // specificDateInput.addEventListener('change', function() {
    //     if (this.checked) {
    //         specificDateContainer.style.display = 'block';
    //     } else {
    //         specificDateContainer.style.display = 'none';
    //     }
    // });

    // // Listen to change event on other radio buttons to hide the specific date container
    // const asapInput = document.getElementById('asap');
    // const flexibleInput = document.getElementById('flexible');

    // asapInput.addEventListener('change', function() {
    //     if (this.checked) {
    //         specificDateContainer.style.display = 'none';
    //     }
    // });

    // flexibleInput.addEventListener('change', function() {
    //     if (this.checked) {
    //         specificDateContainer.style.display = 'none';
    //     }
    // });

      const specificDateCheckbox = document.getElementById('specificDate');
      const specificDateContainer = document.getElementById('specificDateContainer');
      const asapCheckbox = document.getElementById('asap');
      const flexibleCheckbox = document.getElementById('flexible');
      const passwordInput = document.getElementById('password');
      const confirmPasswordInput = document.getElementById('confirmPassword');
      const termsCheckbox = document.getElementById('terms');
      const termsError = document.getElementById('termsError'); // Corrected targeting
  
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
      function validatePasswords() {
          if (passwordInput.value !== confirmPasswordInput.value) {
              passwordInput.classList.add('input-error');
              confirmPasswordInput.classList.add('input-error');
              termsCheckbox.checked = false; // Uncheck terms if passwords don't match
              termsError.innerText = 'Passwords do not match';
              return false;
          } else {
              passwordInput.classList.remove('input-error');
              confirmPasswordInput.classList.remove('input-error');
              termsError.innerText = ''; // Clear error message
              return true;
          }
      }
  
      // Validate terms checkbox
      function validateTerms() {
          if (!termsCheckbox.checked) {
              termsError.innerText = 'You must agree to the terms and conditions';
              return false;
          } else {
              termsError.innerText = ''; // Clear error message
              return true;
          }
      }
  
      // Handle form submission
      document.getElementById('signupForm').addEventListener('submit', function(event) {
          if (!validatePasswords() || !validateTerms()) {
              event.preventDefault(); // Prevent form submission if validation fails
          }
      });
  