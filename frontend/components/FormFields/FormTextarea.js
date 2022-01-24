import { useFormContext } from "react-hook-form";


export default function FormTextarea({ textareaLabel, ...rest }) {
  const { register, formState: { errors } } = useFormContext();
  const { name } = rest;

  return (
    <div>
      <label>{textareaLabel || name}</label>
      <textarea
        {...register(name, { required: rest.required, maxLength: rest.validation.max_length })}
        htmlFor={name}
        id={name}
        placeholder={rest.placeholder}
        {...rest}
      />
    </div>
  );
}