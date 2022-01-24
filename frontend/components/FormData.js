import * as Fields from "./FormFields";
import { useForm, FormProvider } from "react-hook-form";
import { useState } from 'react'

export default function FormData({ fields }) {
  if (!fields) return null;
  const { handleSubmit, ...methods } = useForm();

  // const onSubmit = (values) => console.log(values);

  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);

  if (success) return <p>Form submitted. We'll be in touch!</p>;

  return (
    <FormProvider {...methods} >
      <form >
        {fields.map(({ typename, ...field }, index) => {
          const Field = Fields[typename];

          if (!Field) return null;

          return <Field key={index} {...field} />;
        })}

      </form>
    </FormProvider>
  );
}