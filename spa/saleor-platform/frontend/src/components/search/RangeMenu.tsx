import { useEffect, useState } from "react";

export function RangeMenu({start, range, refine}) {
    
    
    function handleClick() {
        refine(undefined);
    }
    
    return (
        <div className="grid grid-rows-2 divide-y divide-gray-300">
            <div className="flex flex-row justify-between place-items-center gap-5 px-5 py-2">
                <div>
                    The highest price is {range.max}€
                </div>
                <button onClick={handleClick} className="underline">
                    Reset to default
                </button>
            </div>
            <div className="flex flex-col sm:flex-row gap-5 py-1 px-5">
                <RangeInput value={isFinite(start[0]) ? start[0] : undefined} refine={(value) =>refine([value, isFinite(start[1]) ? start[1] : undefined])} placeholder="From" />
                <RangeInput value={isFinite(start[1]) ? start[1] : undefined} refine={(value) => refine([isFinite(start[0]) ? start[0] : undefined, value])} placeholder="To" />
            </div>
        </div>
    )
}

export function RangeInput({ placeholder, refine, value }: { placeholder: string, refine: (value) => void, value: number }) {
    const [currValue, setValue] = useState(value);
    useEffect(()=>setValue(value), [value])
    function handleChange(e) {
        if(e.target.value >= 0){
        refine(e.target.value)
        setValue(e.target.value)
        }
    }
    return (
        <div className="flex flex-row gap-1 place-items-center">
            €
            <div className="border">
                <input type="number" onChange={handleChange} className="pl-3 pr-1 py-2 placeholder:text-stone-700 placeholder:text-xl focus:outline-none w-32" placeholder={placeholder} value={currValue} />
            </div>
        </div>
    )
}