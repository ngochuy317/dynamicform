import { useFormContext } from "react-hook-form";


export default function FormInput({ inputLabel, type: enumType, ...rest }) {
  const { register, formState: { errors } } = useFormContext();
  const { name } = rest;
  const type = enumType.toLowerCase();

  return (
    <div>
      {inputLabel && <label htmlFor={name}>{inputLabel || name}</label>}
      <input
        {...register(name, { required: rest.validation.required, maxLength: rest.validation.max_length })}
        id={name}
        type={type}
        placeholder={rest.placeholder}
        {...rest}
      />
      {errors[name] && errors[name].type === "required" && <span>This is required</span>}
      {errors[name] && errors[name].type === "maxLength" && <span>Max length exceeded</span>}
    </div>
  );
}