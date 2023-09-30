import { useRouter } from "next/router";
import parse from "html-react-parser";
import { useContext, useEffect, useState } from "react";
import { CheckoutContext } from "../../contexts/checkoutContext";
import { useAddToCheckout, useCreateCheckout } from "../../hooks/checkout";
import AddButton from "../../components/buttons/AddButton";
import { PlusIcon, MinusIcon } from '@heroicons/react/24/outline';
import { useGetProductByIdQuery } from "../../../generated/graphql";
import Spinner from "../../components/Spinner";
import ErrorBlock from "../../components/blocks/ErrorBlock";


export default function Product() {
  const [quantity, setQuantity] = useState(1);
  const [loadingState, setLoadingState] = useState(false);
  const { checkoutId, setCheckoutId } = useContext(CheckoutContext);
  const router = useRouter();
  const { createCheckoutMutation, createCheckoutLoading } = useCreateCheckout();
  const { id } = router.query;
  let { addToCheckout, isLoading } = useAddToCheckout({})
  const { data, loading, error } = useGetProductByIdQuery({
    variables: {
      id: id as string
    }
  })
  useEffect(() => {
    if (isLoading || createCheckoutLoading) setLoadingState(true)
    else setLoadingState(false)
  }, [isLoading, createCheckoutLoading])
  async function addToCart() {
    console.log("adding in Checkout");
    console.log("checkoutId " + checkoutId);

    if (checkoutId) {
      console.log("ADDED");
      await addToCheckout({
        variables: {
          checkoutId: checkoutId,
          lines: [{
            variantId: data.product.defaultVariant.id,
            quantity: quantity
          }]
        }
      }).then((data) => {
        console.log(data);
      })
    }
    else {
      console.log("Creating Checkout with this product");

      await createCheckoutMutation({
        variables: {
          input: {
            channel: "default-channel",
            lines: [
              {
                variantId: data.product.defaultVariant.id,
                quantity: quantity
              }
            ]
          }
        }
      })
        .then((data) => {
          console.log(data.data);
          setCheckoutId(data.data.checkoutCreate.checkout.id)
          return data.errors
        })
        .catch((error)=>console.log(error))
    }
  }
  if (error) return <ErrorBlock />
  if (loading) return <Spinner />;
  if (data) {
    const product = data.product
    return (
      <div className="md:grid md:grid-cols-2 mx-20 my-10">
        <div>
          <div className="grid max-w-sm grow rounded overflow px-6">
            <img src={product.thumbnail.url} alt="image" className="w-full group-hover:scale-105 transition" />
          </div>
        </div>
        <ProductSidebar quantity={quantity} setQuantity={setQuantity} product={product} addToCheckout={addToCart} isLoading={loadingState} />
      </div>
    )
  }
}

export function ProductDescription({ children }) {
  return (
    <div className="block font-medium text-gray-700 text-base">
      {children}
    </div>
  )
}

export function ProductSidebar({ quantity, setQuantity, product, addToCheckout, isLoading }) {

  return (
    <div className="flex flex-col gap-4">
      <div className="text-3xl mb-2 group-hover:underline">{product.name}</div>
      <div className="text-start text-xl self-start">${product.pricing.priceRange.stop.gross.amount} {product.pricing.priceRange.stop.gross.currency}</div>
      <ProductQuantity quantity={quantity} setQuantity={setQuantity} />
      <AddButton className="self-start" text={isLoading ? "Loading": "In den Warenkorb liegen"} onClick={addToCheckout} disabled={isLoading ? true : false} />
      <div className="self-start">
        {product.description ? (
          <ProductDescription>
            {JSON.parse(product.description) !== null && parse(JSON.parse(product.description).blocks[0].data.text)}
          </ProductDescription>) : (
          <ProductDescription>
            No description yet
          </ProductDescription>
        )}
      </div>
    </div>
  )
}
export function ProductQuantity({ quantity, setQuantity }) {
  function decreaseQ() {
    if (quantity > 1)
      setQuantity(quantity - 1)
  }
  return (
    <div>
      <div className='flex flex-row gap-4'>
        <div className="flex flex-row gap-4 px-2 border border-black">
          <button data-testid={`decrease-q`} onClick={decreaseQ}>
            <MinusIcon className='h-4 w-4' />
          </button>
          <p data-testid={`quantity`}>{quantity}</p>
          <button data-testid={`increase-q`} onClick={() => setQuantity(quantity + 1)}>
            <PlusIcon className='h-4 w-4' />
          </button>
        </div>
      </div>
    </div>
  )
}