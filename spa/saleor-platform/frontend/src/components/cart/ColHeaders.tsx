export default function ColHeaders() {
    return (
        <div className='flex flex-row gap-3 md:grid md:grid-cols-5 justify-between px-12 py-6 text-gray-400 text-sm'>
            <div className='md:col-span-3'>PRODUCT</div>
            <div className='hidden md:block col-span-1'>Number</div>
            <div className='md:col-span-1'>TOTAL</div>
        </div>
    )
}