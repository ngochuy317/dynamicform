import { useFormContext } from "react-hook-form";

export default function FormSelect({ selectLabel, options, ...rest }) {
  if (!options) return null;

  const { register } = useFormContext();
  const { name } = rest;

  return (
    <div>
      <label htmlFor={name}>{selectLabel || name}</label>
      <select {...register(name, { required: true })} id={name}>
        {options.map(({ option, ...opt }, index) => (
          <option key={index} {...opt}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
}