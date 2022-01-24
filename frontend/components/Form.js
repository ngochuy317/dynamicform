import * as Fields from "./FormFields";
import { useForm, FormProvider } from "react-hook-form";
import { useState } from 'react'

export default function Form({ fields }) {
  if (!fields) return null;
  const { handleSubmit, ...methods } = useForm();

  // const onSubmit = (values) => console.log(values);

  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);

  const onSubmit = async (values) => {
    try {
      const response = await fetch("http://localhost:8080/api/", {
        headers: {
          'Accept': 'application/json, text/plain',
          'Content-Type': 'application/json;charset=UTF-8'
        },
        method: "POST",
        body: JSON.stringify(values),
      });

      if (!response.ok)
        throw new Error(`Something went wrong submitting the form.`);

      setSuccess(true);
    } catch (err) {
      setError(err.message);
    }
  };
  if (success) return <p>Form submitted. We'll be in touch!</p>;

  return (
    <FormProvider {...methods} >
      <form onSubmit={handleSubmit(onSubmit)}>
        {fields.map(({ typename, ...field }, index) => {
          const Field = Fields[typename];

          if (!Field) return null;

          return <Field key={index} {...field} />;
        })}

        <button type="submit">Submit</button>
      </form>
    </FormProvider>
  );
}