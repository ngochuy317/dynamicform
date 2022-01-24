import { useFormContext } from "react-hook-form";

export default function FormCheckbox({ checkboxLabel, ...rest }) {
  const { register } = useFormContext();
  const { name } = rest;

  return (
    <div>
      <label htmlFor={name}>
        <input
          {...register(name, { required: rest.required })}
          id={name}
          type="checkbox"
          required="true"
          checked={rest.checked}
        />
        {checkboxLabel || name}
      </label>
    </div>
  );
}