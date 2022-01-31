import { useState } from "react";
import { UseDataStore } from "../utils/store";

export const useForm = (options) => {
  const setErrorMessage = UseDataStore((state) => state.setErrorMessage);

  const [formData, setFormData] = useState(options?.initialValues || {});
  const [errors, setErrors] = useState({});

  function isEmpty(obj) {
    return Object.keys(obj).length === 0;
  }

  const handleChange = (key, sanitizeFn) => (e) => {
    const value = sanitizeFn ? sanitizeFn(e.target.value) : e.target.value;
    setFormData({
      ...formData,
      [key]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validations = options?.validations;
    if (validations) {
      let valid = true;
      const newErrors = {};
      for (const key in validations) {
        const value = formData[key];
        const validation = validations[key];
        if (validation?.required?.value && !value) {
          valid = false;
          newErrors[key] = validation?.required?.message;
        }

        const pattern = validation?.pattern;
        if (pattern?.value && !RegExp(pattern.value).test(value)) {
          valid = false;
          newErrors[key] = pattern.message;
        }

        const custom = validation?.custom;
        if (custom?.isValid && !custom.isValid(value)) {
          valid = false;
          newErrors[key] = custom.message;
        }
      }

      if (!valid) {
        setErrors(newErrors);

        setErrorMessage({
          isError: true,
          msg:
            "Front-end error: Failed to validate " +
            Object.keys(newErrors).join(", ") +
            ".",
        });

        return;
      }
    }

    setErrors({});

    if (options?.onSubmit) {
      options.onSubmit();
    }
  };

  return {
    formData,
    handleChange,
    handleSubmit,
    errors,
  };
};
