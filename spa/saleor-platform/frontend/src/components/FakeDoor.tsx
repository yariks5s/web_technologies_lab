import Image from 'next/image';

export default function FakeDoor(){
    return(
        <div className="flex flex-col place-items-center my-auto text-2xl">
            <div>Unfortunately, this feature has not yet been implemented.</div>
            <div>Thank you that you are interested in our products.</div>
            <Image src={"/dog.gif"} width={100} height={100} alt={"dog thanking to customer GIF"}/>
        </div>
    )
}