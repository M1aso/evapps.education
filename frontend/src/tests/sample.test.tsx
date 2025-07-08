import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'

function Hello() {
  return <div>Hello World</div>
}

describe('Hello', () => {
  it('renders text', () => {
    render(<Hello />)
    expect(screen.getByText('Hello World')).toBeInTheDocument()
  })
})
